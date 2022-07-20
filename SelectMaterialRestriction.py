from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    # アンドゥを開始
    doc.StartUndo();

    # アクティブオブジェクトを取得する
    op = doc.GetActiveObject()

     # アクティブオブジェクトが無い場合終了
    if not op: return

    # ポリゴンオブジェクトでない場合終了
    if op.GetType() != c4d.Opolygon: return

    # オブジェクトの最初のタグを取得
    tag = op.GetFirstTag()
    
    # アンドゥを記録
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, op)
    
    # オブジェクトの選択を解除
    polySelection = op.GetPolygonS()
    polySelection.DeselectAll()

    # ポリゴン選択範囲タグのリストにポリゴン選択範囲タグを格納
    polySelectionTags = []
    getPolygonSelectionTags(tag, polySelectionTags)
    
    # 最初のタグをセットする
    tag = op.GetFirstTag()
    while(tag):
        
        # マテリアルタグを探す
        if (tag.GetType() == c4d.Ttexture):
            
            # マテリアルタグの’選択範囲に限定’が設定してあるかどうか
            if tag[c4d.TEXTURETAG_RESTRICTION]:
                
                # ポリゴン選択範囲タグ格納用リストから一致する選択範囲タグがあるかどうか調べる
                for poluSelectionTag in polySelectionTags:
                    
                    # 選択版に限定しているタグがあった場合
                    if(tag[c4d.TEXTURETAG_RESTRICTION] == poluSelectionTag[c4d.ID_BASELIST_NAME]):
                
                        # 選択範囲をマージする
                        mergeSelection(poluSelectionTag, polySelection)
                    
        
        # 次のタグへ      
        tag = tag.GetNext()   
           

    # アンドゥ終了ポイント
    doc.EndUndo()

    # エディタを更新
    op.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()
    
    return

# ポリゴン選択範囲タグをリストに追加する
def getPolygonSelectionTags(tag, tags):
    # オブジェクトのタグを全て調べる
    while(tag):

        # ポリゴン選択範囲タグの場合
        if tag.GetType() == c4d.Tpolygonselection:

            tags.append(tag);


        # 次のタグへ
        tag = tag.GetNext()
    
    return

# 選択範囲をマージする関数
def mergeSelection(tag, polygons):
    # 選択を取得
    selection = tag.GetBaseSelect()

    # タグの選択範囲をマージ
    polygons.Merge(selection)
    
    return
    
"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()