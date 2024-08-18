import logging
import MeCab
import ipadic
import re

translation_table = {
    '2m': 'ツーメーター',
    '6m': 'シックスメーター',
    '10m': 'テンメーター',
    '15m': 'じゅうごメーター',
    '20m': 'にじゅうメーター',
    '40m': 'よんじゅうメーター',
    '80m': 'はちじゅうメーター',
    '160m': 'ひゃくろくじゅうメーター',
    'achievement': 'アチーブメント',
    'activation' : 'アクティベーション',
    'activations' : 'アクティベーション',
    'activator' : 'アクティベーター',
    'activators' : 'アクティベーター',
    'account': 'アカウント',
    'add' : 'アド',
    'adif' : 'エイディフ',
    'air': 'エアー',
    'alert' : 'アラート',
    'alerts': 'アラート',
    'alexloop': 'アレックスループ',
    'alltrails': 'オールトレイルズ',
    'and' : 'アンド',
    'antenna': 'アンテナ',
    'antennas': 'アンテナ',
    'anywhere': 'エニィフェア',
    'app': 'アップ',
    'award' : 'アワード',
    'awards': 'アワード',
    'band': 'バンド',
    'bandspringer': 'バンドスプリンガー',
    'bronze': 'ブロンズ',
    'buddipole': 'バディポール',
    'buddistick': 'バディスティック',
    'by': 'バイ',
    'callsign': 'コールサイン',
    'certificate': 'サーティフィケイト',
    'certificates': 'サーティフィケイト',
    'chaser' : 'チェイサー',
    'chasers' : 'チェイサー',
    'chasing': 'チェイシング',
    'call' : 'コール',
    'calling' : 'コーリング',
    'comment': 'コメント',
    'comments': 'コメント',
    'complete': 'コンプリート',
    'create': 'クリエイト',
    'chameleon': 'カメレオン',
    'choose': 'チューズ',
    'cluster' : 'クラスター',
    'coil': 'コイル',
    'coils': 'コイルズ',
    'database' : 'データベース',
    'date': 'デート',
    'defined': 'デファインド',
    'deluxe': 'デラックス',
    'dipole': 'ダイポール',
    'discovery': 'ディスカバリー',
    'elecraft': 'エレクラフト',
    'end': 'エンド',
    'fed': 'フェッド',
    'end-fedz': 'エンドフェッズ',
    'enter': 'エンター',
    'entry' : 'エントリ',
    'explorer': 'エクスプローラー',
    'fast': 'ファスト',
    'file': 'ファイル',
    'friendly': 'フレンドリー',
    'gaia' : 'ガイア',
    'goat': 'ゴート',
    'gold': 'ゴールド',
    'ground': 'グラウンド',
    'half': 'ハーフ',
    'ham' : 'ハム',
    'hamalert': 'ハムアラート',
    'hamlog': 'ハムログ',
    'happy': 'ハッピー',
    'hole' : 'ホール',
    'honour' : 'オナー',
    'hopper': 'ホッパー',
    'icom': 'アイコム',
    'ii': 'ツー',
    'iii': 'スリー',
    'is' : 'イズ',
    'it': 'イット',
    'kenwood':'ケンウッド',
    'labs': 'ラボラトリーズ',
    'log' : 'ログ',
    'logbook': 'ログブック',
    'logs' : 'ログ',
    'logger': 'ロガー',
    'logging': 'ロギング',
    'loop': 'ループ',
    'map': 'マップ',
    'mapping': 'マッピング',
    'mountain': 'マウンテン',
    'modular': 'モジュラー',
    'milestone': 'マイルストン',
    'milestones': 'マイルストン',
    'mini': 'ミニ',
    'mkii': 'マークツー',
    'mkiii': 'マークスリー',
    'my' : 'マイ',
    'myantennas': 'マイアンテナズ',
    'official' : 'オフィシャル',
    'other' : 'アザー',
    'package': 'パッケージ',
    'packages': 'パッケージズ',
    'packtenna': 'パックテナ',
    'par': 'パー',
    'park': 'パーク',
    'parks': 'パークス',
    'plane': 'プレーン',
    'point' : 'ポイント',
    'points' : 'ポイント',
    'portable': 'ポータブル',
    'pota':'ポタ',
    'precision': 'プレシジョン',
    'project': 'プロジェクト',
    'propagaion': 'プロパゲーション',
    'radio': 'ラディオ',
    'reference': 'リファレンス',
    'references': 'リファレンス',
    'register': 'レジスター',
    'river': 'リバー',
    'roll' : 'ロール',
    's2s': 'エスツーエス',
    'save': 'セーブ',
    'shack': 'シャック',
    'silver': 'シルバー',
    'single': 'シングル',
    'site' : 'サイト',
    'sites': 'サイト',
    'sloth': 'スロース',
    'software': 'ソフトウェア',
    'sota' : 'ソタ',
    'sotabeams': 'ソタビームス',
    'sotawatch' : 'ソタウォッチ',
    'spot' : 'スポット',
    'spots': 'スポット',
    'spotting' : 'スポッティング',
    'spotter': 'スポッター',
    'standing': 'スタンディング',
    'submit': 'サブミット',
    'summit': 'サミット',
    'summits': 'サミット',
    'summits on the air' : 'サミットオンジエアー',
    'super': 'スーパー',
    'system': 'システム',
    'systems': 'システム',
    'take': 'テイク',
    'the' : 'ジ',
    'this': 'ディス',
    'trail': 'トレイル',
    'upload': 'アップロード',
    'vagabond': 'バガボンド',
    'vertical': 'バーチカル',
    'walkham': 'ウォークハム',
    'watch': 'ウォッチ',
    'website' : 'ウェブサイト',
    'wolf': 'ウォルフ',
    'xiegu': 'シェーグー',
    'yaesu': 'ヤエス',
    'yamap': 'ヤマップ',
    'zone': 'ゾーン',
    '##': ' ',
    '###': ' ',
    '####': ' ',
    ',': ', ',
    '--': ' ',
    '---': ' ',
    '----': ' ',
    '**': '',
}

logger = logging.getLogger(__name__)

chunk_buffer = ""

def sota_translation(content: str) -> str:
    global chunk_buffer
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)
    content = re.sub(r'\*\*','',content)
    content , chunk_buffer = remove_urls_from_chunk(content, chunk_buffer)
    content_lines = content.split('\n')
    translation_result = []
    for line in content_lines:
        nodes = []
        node = mecab.parseToNode(line)
        prev = None
        while node:
            s:str = node.surface 
            if s.isdigit():
                prev = s
                node = node.next
                continue
            if prev:
                if s == 'm':
                    alt = int(prev)
                    if alt >= 150 and alt <= 3776:
                        nodes.append(prev + 'メートル')
                    else:
                        nodes.append(prev + s)
                else:
                    nodes.append(prev)
                    nodes.append(s)
                prev = None
                node = node.next
                continue
            else:
                nodes.append(s)
                node = node.next

        replaced_line = [translation_table.get(node.lower(), node) for node in nodes if node]
        #logger.warning(f"chunk replaced = {replaced_line}")
        translation_result.append(''.join(replaced_line))

    result = '\n '.join(translation_result)
    #logger.warning(f"translation result = {content} ->\n{result}")
    return result

def remove_urls_from_chunk(chunk, buffer=""):
    url_pattern = re.compile(r'https?:[^\s()]+')
    combined = buffer + re.sub(r'（|）',' ',chunk)
    matches = list(url_pattern.finditer(combined))
    if matches:
        cleaned_chunk = url_pattern.sub(r'', combined)
        removed = 0
        for m in matches:
            start, end = m.span()
            if start > len(buffer):
                break
            if end > len(buffer):
                removed += len(buffer) - start
            else:
                removed += end - start
        cleaned_chunk = cleaned_chunk[len(buffer)-removed:]
        return cleaned_chunk, chunk
    else:
        return chunk, ""
