class AddSectionToProducts < ActiveRecord::Migration[5.0]
  def change
    add_column :products, :section, :string
  end
end
