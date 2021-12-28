--Table: Users
Drop table users_address;
Drop table user_coupons;
Drop table operating_hours;
Drop table restaurant_coupons;
Drop table restaurant_address;
Drop table reviews;
Drop table address;
Drop table reservations;
Drop table amenities;
Drop table restaurant;
Drop table coupons;
Drop table users;


create table users(
email char(128) primary key,
phone char(10),
name varchar(128),
Dob date
);


--Table: Address


create table address(
address_line varchar(128),
city char(64),
state char(64),
zipcode integer,
Primary key(address_line, city)
);


--Table: Restaurants



Create table restaurant(
Restaurant_id char(32) primary key,
restuarant_name varchar(128),
cost real
);


--Table: Addresses of userss

Create table users_address(
U_email char(128),
Address_line varchar(128),
City char(64),
Primary key(u_email, address_line, city),
Foreign key(u_email) references users(email)
);


--Table: Address of restaurant


Create table restaurant_address(
Reataurant_id char(32) primary key,
Address_line varchar(128),
City char(64),
Foreign key(Reataurant_id) references Restaurant(restaurant_id)
);


--Table: reviews



create table reviews(
ambience integer check (ambience <= 5 and ambience >= 0),
food_quality integer check (food_quality <= 5 and food_quality >= 0),
service integer check (service <= 5 and service >= 0),
overall_experience integer check (overall_experience <= 5 and overall_experience >= 0),
Description varchar(256),
User_email char(128),
Restaurant_id char(32),
Primary key (User_email, Restaurant_id),
Foreign key(user_email) references users(email),
Foreign key(Restaurant_id) references restaurant(restaurant_id)
);


--Table:Reservations


Create table reservations(
date_reserved date,
time_reserved time,
Table_no integer,
User_email char(128),
Restaurant_id char(32),
Primary key(user_email, restaurant_id),
Foreign key(User_email) references users(email),
Foreign key(Restaurant_id) references restaurant(restaurant_id)
);


--Table: Operating hours



Create table operating_hours(
Restaurant_id char(32),
Day char(10),
Time char(12),
Primary key(restaurant_id, day, time),
Foreign key(restaurant_id) references restaurant(restaurant_id) on delete cascade
);


--Table: Amenities


Create table amenities(
Restaurant_id char(32) primary key,
Wifi char(1),
Parking char(1),
Wheelchair char(1),
Alcohol char(64),
Foreign key(restaurant_id) references restaurant(restaurant_id) on delete cascade
);


--Table: Coupons 


Create table coupons(
Coupon_id char(32) primary key,
Expiry_date date,
Discount_amt real
);


--Table: User coupons


Create table user_coupons(
user_email char(128),
Coupon_id char(32),
Primary key(user_email, coupon_id),
Foreign key(User_email) references users(email),
Foreign key(coupon_id) references coupons(Coupon_id)
);


--Table: Restaurant coupons


Create table restaurant_coupons(
Restaurant_id char(32),
Coupon_id char(32),
Primary key(restaurant_id, coupon_id),
Foreign key(restaurant_id) references restaurant(restaurant_id),
Foreign key(coupon_id) references coupons(Coupon_id)
);
