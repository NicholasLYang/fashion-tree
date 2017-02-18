# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
require 'csv'

csv_text = File.read(Rails.root.join('lib', 'seeds', 'handm.csv'))
csv = CSV.parse(csv_text, :headers => true, :encoding => 'ISO-8859-1')
csv.each do |row|
  puts row['price']
  p = Product.new
  p.picture = row['picture']
  p.price = row['price'][1..-1]
  p.score = row['score']
  p.link = row['link']
  p.keyword = row['keyword']
  p.name = row['name']
  p.material = row['material']
  p.save
end
