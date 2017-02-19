# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
require 'csv'
Dir.glob(Rails.root.join('lib', 'seeds', 'products', "*.csv")) do |f|
  puts f
  csv_text = File.read(f)
  csv = CSV.parse(csv_text, :headers => true, :encoding => 'ISO-8859-1')
  csv.each do |row|
    next if row['score'] == nil
    p = Product.new
    p.picture = row['picture']
    p.price = row['price'][1..-1]
    p.score = row['score']
    p.link = row['link']
    p.keyword = row['keyword']
    p.name = row['name']
    p.material = row['material']
    p.section = row['section']
    p.brand = row['brand']
    p.save
  end
end

csv_text = File.read(Rails.root.join('lib', 'seeds', 'devices', 'newegg.csv'))
csv = CSV.parse(csv_text, :headers => true, :encoding => 'ISO-8859-1')
csv.each do |row|
  wattage = row['watts'].to_f
  next if wattage == 0.0 || wattage == nil
  d = Device.new
  d.picture = row['picture']
  d.score = row['score']
  d.link = row['link']
  d.keyword = row['keyword']
  d.name = row['name']
  d.keyword = row['keyword']
  d.brand = row['brand']
  d.watts = wattage
  d.save
end
