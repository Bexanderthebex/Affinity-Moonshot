use affinity;

drop table if exists campaign;
drop table if exists user;
drop table if exists campaign_user;

create table campaign (
    id int auto_increment primary key not null,
    name varchar(256) not null,
    description varchar(256) not null,
    age int not null,
    gender varchar(256) not null,
    network varchar(256) not null, 
    location varchar(256) not null
);

create table user (
    id int auto_increment primary key not null,
    username varchar(256) not null,
    age int not null,
    location varchar(256) not null,
    password varchar(256) not null
);

create table campaign_user (
    user_id int not null,
    campaign_id int not null,
    link varchar(256) not null
);