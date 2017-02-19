class AddKarmaToUsers < ActiveRecord::Migration[5.0]
  def change
    add_column :users, :karma, :integer
  end
end
