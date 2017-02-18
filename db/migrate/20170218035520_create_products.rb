class CreateProducts < ActiveRecord::Migration[5.0]
  def change
    create_table :products do |t|
      t.string :picture
      t.float :price
      t.integer :score
      t.string :link
      t.string :material

      t.timestamps
    end
  end
end
