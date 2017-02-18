class AddNameToProducts < ActiveRecord::Migration[5.0]
  def change
    add_column :products, :name, :string
  end
end
