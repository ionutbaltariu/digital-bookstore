package pos.auth.Jwt;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import pos.auth.Entities.UserEntity;
import pos.auth.Repositories.UserRepository;


@Service
public class JwtUserDetailsService implements UserDetailsService {
    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        List<UserEntity> usersWithGivenUsername = userRepository.findByUsername(username);
        UserEntity user;
        if(!usersWithGivenUsername.isEmpty()){
            user = usersWithGivenUsername.get(0);
            return new User(user.getUsername(), user.getPassword(), new ArrayList<>());
        }
        else{
            throw new UsernameNotFoundException("User not found with username: " + username);
        }
    }
}