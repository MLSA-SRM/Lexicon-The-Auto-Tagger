const LocalStrategy = require('passport-local').Strategy;
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

// user models

const User = require('../models/User');


module.exports = function(passport){
    passport.use(
        new LocalStrategy({ usernameField:'email'}, (email, password, done) => {
            //match user
            User.findOne({ email : email})
            .then(user => {
                if(!user){
                    return done(null, false, {message :'That email is not registered'} );
                }

                //match password
                bcrypt.compare(password, user.password, (err, isMatch) => {
                    if(err) throw err;
                    if(isMatch){
                        return done(null, user);
                    }else{
                        return done(null, false, {message : 'Password Incorrect'} );
                    }
                });
            })
            .catch(err => console.log(err));

        })
    );
    passport.serializeUser((user, done) => {
        done(null, user.id);
      });
      
      passport.deserializeUser((id, done) => {
        User.findById(id, (err, user) => {
          done(err, user);
        });
      });
}