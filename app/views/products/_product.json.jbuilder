json.extract! product, :id, :picture, :price, :score, :link, :material, :created_at, :updated_at
json.url product_url(product, format: :json)