class CreateDevices < ActiveRecord::Migration[5.0]
  def change
    create_table :devices do |t|
      t.string :name
      t.string :link
      t.float :price
      t.integer :score
      t.float :watts
      t.string :picture
      t.string :keyword

      t.timestamps
    end
  end
end
