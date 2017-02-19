class AddBrandToDevices < ActiveRecord::Migration[5.0]
  def change
    add_column :devices, :brand, :string
  end
end
