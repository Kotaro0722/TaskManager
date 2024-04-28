# 【基本仕様】

- １．課題の登録

  - それぞれのスレッド内で以下の方法で課題を登録する。
    【内容】[日付(月/日 時間:分)]
  - 課題の登録が完了した場合は ⭕ リアクションを付与する

- 2.課題の完了
  - ユーザが ✅ のリアクションを付ける。
- 3.課題の催促
  - 期限の 1 日前でも ✅ のリアクションを付けていなかったユーザにメンションをする。
  - この時メンションするメンバーはスレッドに参加しているメンバのみとする。

# 【データベース仕様】

- １．課題管理テーブル
  | message_id | channel_id | thread_id | deadline |
  | BIGINT, PK | BIGINT, NN | BIGINT | DATE,NN |

  - 登録された課題のうち、期限が過ぎていない課題のみを保存する
  - 期限が過ぎた課題は削除する

- ２．スレッドメンバ管理テーブル
  | id | thread_id | member_id | created_date |
  | AU,PK,INT | BIGINT,BIGINT | BIGINT,BIGINT | DATE |

  - 各スレッドに属している人が保存される
  - スレッドに新しく入った人がいたら更新する
  - created_date から 1 年以上経過したものは削除する
