package pos.auth.Jwt;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pos.auth.DTO.UserDTO;
import pos.auth.Entities.UserEntity;
import pos.auth.Repositories.UserRepository;


@Service
public class JwtUserDetailsService {
    @Autowired
    private UserRepository userRepository;

    public UserDTO loadUserByUsername(String username) throws Exception {
        List<UserEntity> usersWithGivenUsername = userRepository.findByUsername(username);
        UserEntity user;
        if(!usersWithGivenUsername.isEmpty()){
            user = usersWithGivenUsername.get(0);
            return new UserDTO(user.getUsername(), user.getPassword(), user.getRole());
        }
        else{
            throw new Exception("User not found with username: " + username);
        }
    }
}