package pos.auth.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Jwt.JwtTokenUtil;
import pos.auth.Jwt.JwtUserDetailsService;
import pos.auth.Repositories.UserRepository;
import pos.auth.soap.LoginRequest;
import pos.auth.soap.LoginResponse;
import org.springframework.security.crypto.bcrypt.BCrypt;

@Endpoint
public class AuthService {
    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Autowired
    private JwtUserDetailsService userDetailsService;

    @Autowired
    private UserRepository userRepository;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/Auth";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "loginRequest")
    @ResponsePayload
    public LoginResponse login(@RequestPayload LoginRequest input) throws Exception {
        final UserDetails userDetails = userDetailsService
                .loadUserByUsername(input.getName());
        LoginResponse r = new LoginResponse();
        if(!BCrypt.checkpw(input.getPassword(), userDetails.getPassword())){
            throw new Exception("WRONG_PASSWORD");
        }
        else{
            authenticate(input.getName(), input.getPassword());

            final String token = jwtTokenUtil.generateToken(userDetails);
            r.setToken(token);
            return r;
        }
    }

    private void authenticate(String username, String password) throws Exception {
        try {
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(username, password));
        } catch (DisabledException e) {
            throw new Exception("USER_DISABLED", e);
        } catch (BadCredentialsException e) {
            throw new Exception("INVALID_CREDENTIALS", e);
        }
    }
}
