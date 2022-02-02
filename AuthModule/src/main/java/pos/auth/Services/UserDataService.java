package pos.auth.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pos.auth.Model.DTO.UserWithProfileDTO;
import pos.auth.Model.Entities.UserEntity;
import pos.auth.Model.Entities.UserProfileEntity;
import pos.auth.Model.Repositories.UserProfileRepository;
import pos.auth.Model.Repositories.UserRepository;

import java.util.List;
import java.util.Optional;

@Service
public class UserDataService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserProfileRepository userProfileRepository;

    public UserWithProfileDTO loadUserWithProfileData(int id) throws Exception{
        Optional<UserEntity> correspondentUser = userRepository.findById(id);
        List<UserProfileEntity> correspondentUserProfileContainer = userProfileRepository.findUserProfileEntityByUserid(id);

        checkIfUserAndProfileExists(correspondentUser, correspondentUserProfileContainer);

        UserProfileEntity correspondentUserProfile = correspondentUserProfileContainer.get(0);

        return new UserWithProfileDTO(correspondentUserProfile.getFirstname(),
                correspondentUserProfile.getLastname(),
                correspondentUser.get().getUsername(),
                correspondentUserProfile.getEmail(),
                correspondentUserProfile.getAddress(),
                correspondentUserProfile.getBirthday().toString());
    }

    void checkIfUserAndProfileExists(Optional<UserEntity> userEntity,
                                     List<UserProfileEntity> userProfileEntityContainer) throws Exception{
        if(userEntity.isEmpty())
            throw new Exception("User with the given id was not found.");

        if(userProfileEntityContainer.isEmpty())
            throw new Exception("The given user does not have a profile created.");
    }

}
