class AddSectionToDevices < ActiveRecord::Migration[5.0]
  def change
    add_column :devices, :section, :string
  end
end
