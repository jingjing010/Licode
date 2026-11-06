# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"nlaebolko"\n', '1'), ('"loonbalxballpoon"\n', '2'), ('"balloon"\n', '1'), ('"balloonballoon"\n', '2'), ('"z"\n', '0'), ('"yo"\n', '0'), ('"nzy"\n', '0'), ('"onlnllo"\n', '0'), ('"nloxloyyoxzblozn"\n', '0'), ('"xyxnlloayloyxllxannlyblllzlloob"\n', '2'), ('"olozyoxyxxzlonnzlzxzzazxonyaoolyoazloolxllnlnzlznlznoablyalzaloyybblozblylbzxollazonzbnnoloonzlozlol"\n', '6'), ('"oaaollobbobolooaoablaoxllaolyxazoxbzzooybobaloxnllyozooynolbyoboxyalblyoyoxanlooxllybyozzxlbnallnlxnynzalzlllzzalnolxblaxzooanzlzaalzollxxlllbnbbbballzoooaoxyoxloxxllxoybaxbyloyolbnloolllozyzbbnlayoxlbolooayozlxxxzlaooaxbbonnzxxooolllybzlybbanblblxxolaboobblolxnanaxaanoblllylbloxlbnnxnxbnalnbllzolanaxnbzlooolxlaooyxzzonzzaznyblzlaoyzxlooyxnzzlznooloboxllzlblnxlonollnxzoaoxazozzalyaozlobzoyzyloalxloyznbnlbazxalyolaoxloolozallnolllxollbaxloxanlylyznblolololoolzzlllaboooaoynxanlllooollnynybollalxzylnnoxalzozlaooaoaloolxxoybaxzlolaozzxzlboloozlolabanonooyoylnoloyzananxyblylonlzyaaxobzzxoalzzoyxbollylyollllnloloolbxzooxzlxbxxzylzozxlaooxoaxbolzaxaxlyaxlybooloaxalllzxlnolnlbozllaxlblxnnylxnxynooznolzlozooybyoxloyollnoooolzxllloyolylblnyxybablxzlzoazbaonolozoxxynlbbxllzlblaoaxnxyloynbonxlnnoaanznnlnoannlonzxbxllyxxyalblbnxxnxazyaxoonxzozbololllllbxolxoyolynoxlaxblzaxbxooozxbnzoaoallyyxnylzbxxabzloaaoboloozoolaolollbalooaalnyzxlolllyxxolbxboaoazyyxzylybxonzlyalbnylazlyoxyolbbyxlyolzbnloybloboa"\n', '83')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
