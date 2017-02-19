Rails.application.routes.draw do
  devise_for :users
  resources :devices
  get 'about/index'

  resources :products
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  get 'welcome/index'
  root 'welcome#index'
end
