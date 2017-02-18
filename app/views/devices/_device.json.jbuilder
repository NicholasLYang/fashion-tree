json.extract! device, :id, :name, :link, :price, :score, :watts, :picture, :keyword, :created_at, :updated_at
json.url device_url(device, format: :json)