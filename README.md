# Copilot Studio で始める Agent Skills 勉強会

Microsoft Copilot Studio の GitHub Copilot エージェントで Agent Skills を作成・使用する勉強会（講義＋ハンズオン、180分）の資料一式です。

## 資料

| 資料 | 内容 |
|---|---|
| [スライド](https://seiyatogawa.github.io/copilot-studio-agent-skills-workshop/) | 講義用のスライド（ブラウザで表示。← → で移動、F で全画面） |
| [handson/README.md](handson/README.md) | ハンズオンの手順書（Step 0〜6、コピー用の文面つき） |
| [handson/dist/](handson/dist/) | ハンズオンでアップロードするスキル（`.md` / `.zip`） |

## アジェンダ

| # | パート | 内容 | 時間 |
|---|---|---|---|
| 0 | はじめに | 本日のゴール | 5分 |
| 1 | Agent Skills とは | 定義・フォルダ構成・段階的な読み込み | 15分 |
| 2 | Copilot Studio での位置づけ | 指示／ナレッジ／ツールとの違い、呼び出しの仕組み | 10分 |
| 3 | 追加方法と管理 | AI で生成（デモ）、Step 0〜3：エージェント作成・最初から作成・.md アップロード・.zip 置換 | 45分 |
| 4 | 書き方と注意点 | フロントマター、description、トラブル対応 | 15分 |
| - | 休憩 | | 10分 |
| 5 | 演習 | Step 4〜5：作成したスキルの動作確認と振り返り | 20分 |
| 6 | 公開スキルの活用 | 公開リポジトリと取り込み前の確認事項 | 10分 |
| 7 | 自分たちでスキルを作成 | Step 6：業務の選定・設計・作成・テスト・共有 | 35分 |
| 8 | まとめ・Q&A | | 15分 |

## 前提条件

- Copilot Studio で **GitHub Copilot エージェント** を作成できる環境
- その環境に **Copilot クレジット** が割り当てられていること

## フォルダ構成

```text
.
├── deck/                        … スライド（index.html と画像）
└── handson/
    ├── README.md                … 手順書
    ├── dist/                    … 配布物（アップロード用の .md / .zip）
    ├── expense-policy-check/    … サンプルスキルの原本（zip の中身）
    └── build_dist.py            … dist/ の再生成スクリプト
```

## 注意事項

- 画面キャプチャと手順は 2026 年 9 月時点の Copilot Studio に基づきます。画面や動作は変更される場合があります。最新情報は [Microsoft Learn](https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/agents-experience/skills-overview) を参照してください。
- サンプルの経費精算規程は、ハンズオン用に作成した架空のものです。

## ライセンス

[MIT License](LICENSE)
