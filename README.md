# Summer Invitational Data Open 2020

Github for the team composed of: Khaoula Belahsen, Patrick Saux, Reda Arab and Louis Lapassat.

### Rules

 - Each member works on his **own branch**.
 - When you finish something merge it to **master**.
 
 ### Tools
 
  - Change branch with: git checkout name_of_the_branch
  - Create a new branch from another branch: git checkout -b my_new_branch from_this_branch
  - Update your branch on Github: 
      - select what you want to add: git add file_1 file_2 file_3 
      - commit your push: git commit -m"here_write_something_about_your_commit"
      - push your commit: git push
      - if it's the first time you push for this branch you may have to follow what the terminal is saying: git push -u origin my_new_branch
   - If you want to update your branch with another branch: git rebase another_branch (you will have to force the push: git push -f)
   - If you want to select only particular commits: git cherry-pick commit_id
   
