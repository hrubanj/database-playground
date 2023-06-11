create table "user"
(
    id    int       primary key,
    name  varchar(255) not null,
    address varchar(255) not null,
    email varchar(255) not null
);


create table "visit"
(
    id         int       primary key,
    user_id    int          not null,
    site_id    int          not null,
    timestamp  timestamp    not null,
    post_id    int          not null,
    origin_url varchar(255) not null,
    ip         varchar(255) not null,
    user_agent varchar(255) not null
);

create table "post"
(
    id           int       primary key,
    user_id      int          not null,
    time_created timestamp    not null,
    time_updated timestamp    not null,
    title        varchar(255) not null,
    content      text         not null
);



create table "comment"
(
    id              int    primary key,
    user_id         int       not null,
    post_id         int       not null,
    time_created    timestamp not null,
    time_updated    timestamp not null,
    content         text      not null,
    upvotes_count   int       not null,
    downvotes_count int       not null
);