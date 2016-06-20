#!/bin/csh

cd /Users/belcher/Desktop/NOAA_CSC/CLMDIV/CMB_Anom/Images

#Upload all of the images
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Temperature/620/* ubuntu@107.20.157.228:/var/www/Images/averagetempanom-monthly-cmb/620/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Temperature/1000/* ubuntu@107.20.157.228:/var/www/Images/averagetempanom-monthly-cmb/1000/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Temperature/diy/* ubuntu@107.20.157.228:/var/www/Images/averagetempanom-monthly-cmb/diy/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Temperature/hd/* ubuntu@107.20.157.228:/var/www/Images/averagetempanom-monthly-cmb/hd/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Temperature/hdsd/* ubuntu@107.20.157.228:/var/www/Images/averagetempanom-monthly-cmb/hdsd/

scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Precipitation/620/* ubuntu@107.20.157.228:/var/www/Images/precipanom-monthly-cmb/620/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Precipitation/1000/* ubuntu@107.20.157.228:/var/www/Images/precipanom-monthly-cmb/1000/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Precipitation/diy/* ubuntu@107.20.157.228:/var/www/Images/precipanom-monthly-cmb/diy/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Precipitation/hd/* ubuntu@107.20.157.228:/var/www/Images/precipanom-monthly-cmb/hd/
scp -i /Users/belcher/AwsFiles/NewEarl.pem ./Precipitation/hdsd/* ubuntu@107.20.157.228:/var/www/Images/precipanom-monthly-cmb/hdsd/

#Now for local cleanup
rm ./Temperature/*/*
rm ./Precipitation/*/*

exit