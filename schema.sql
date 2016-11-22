drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  name text not null,
  email text not null,
  password text not null,
  CONSTRAINT email_unique UNIQUE (email)
);
