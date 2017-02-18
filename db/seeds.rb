# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
products = Product.create([
                            {picture: 'http://lp.hm.com/hmprod?set=key[source],value[/model/2016/E00%200317980%20005%2030%201243.jpg]&set=key[rotate],value[]&set=key[width],value[]&set=key[height],value[]&set=key[x],value[]&set=key[y],value[]&set=key[type],value[STILL_LIFE_FRONT]&set=key[hmver],value[6]&call=url[file:/product/large',
                             price: 18,
                             score: 20,
                             link: "https://www.horriblyunderqualified.com",
                             material: "Gold",
                             name: "Shoe"}
                          ])
