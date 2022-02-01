package pos.auth.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Model.Entities.UserEntity;
import pos.auth.Model.Entities.UserProfileEntity;
import pos.auth.Model.Repositories.UserProfileRepository;
import pos.auth.Model.Repositories.UserRepository;
import org.springframework.security.crypto.bcrypt.BCrypt;
import pos.auth.View.Register.RegisterRequest;
import pos.auth.View.Register.RegisterResponse;

import java.sql.Date;
import java.util.List;

@Endpoint
public class RegisterController {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserProfileRepository userProfileRepository;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/register";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "registerRequest")
    @ResponsePayload
    public RegisterResponse register(@RequestPayload RegisterRequest input) throws Exception {
        RegisterResponse r = new RegisterResponse();

        if(input.getPassword().length() < 8){
            r.setStatus("Registration failed.");
            r.setErrorMessage("Password has less than 8 characters.");
        }
        else if(input.getName().length() < 4){
            r.setStatus("Registration failed.");
            r.setErrorMessage("Username has less than 4 characters.");
        }
        else{
            UserEntity user = new UserEntity();
            user.setUsername(input.getName());
            user.setPassword(BCrypt.hashpw(input.getPassword(), BCrypt.gensalt(10)));
            user.setRole("User");

            try{
                userRepository.save(user);
                userProfileRepository.save(getUserProfileFromRequestInput(input));
                r.setStatus("Registered. You may log in.");
            }
            catch(Exception e){
                if(e.getMessage().contains("users_UN")){
                    r.setStatus("Registration failed.");
                    r.setErrorMessage("Username already exists. Please pick another.");
                }
                else{
                    r.setStatus("Registration failed.");
                    r.setErrorMessage("Could not save the user in the database.");
                }
            }
        }

        return r;
    }

    UserProfileEntity getUserProfileFromRequestInput(RegisterRequest input){
        UserProfileEntity userProfile = new UserProfileEntity();

        userProfile.setFirstname(input.getFirstname());
        userProfile.setLastname(input.getLastname());
        userProfile.setEmail(input.getEmail());
        userProfile.setAddress(input.getAddress());
        userProfile.setBirthday(Date.valueOf(input.getBirthday()));
        List<UserEntity> insertedUser = userRepository.findByUsername(input.getName());
        userProfile.setUserid(insertedUser.get(0).getId());

        return userProfile;
    }
}
