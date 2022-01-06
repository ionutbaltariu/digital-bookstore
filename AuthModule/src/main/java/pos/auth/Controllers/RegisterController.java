package pos.auth.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Model.Entities.UserEntity;
import pos.auth.Model.Repositories.UserRepository;
import org.springframework.security.crypto.bcrypt.BCrypt;
import pos.auth.View.Register.RegisterRequest;
import pos.auth.View.Register.RegisterResponse;

@Endpoint
public class RegisterController {
    @Autowired
    private UserRepository userRepository;

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
}
