# config valid only for current version of Capistrano
lock "3.7.1"

set :application, "fashion-tree"
set :repo_url, "git@github.com:NicholasLYang/fashion-tree.git"

set :deploy_to, '/home/deploy/fashion-tree'

append :linked_files, "config/database.yml", "config/secrets.yml"
append :linked_dirs, "log", "tmp/pids", "tmp/cache", "tmp/sockets", "vendor/bundle", "public/system", "public/uploads"
