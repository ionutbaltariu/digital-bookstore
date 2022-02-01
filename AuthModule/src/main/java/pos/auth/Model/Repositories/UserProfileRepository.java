package pos.auth.Model.Repositories;

import org.springframework.data.repository.CrudRepository;
import pos.auth.Model.Entities.UserProfileEntity;

import java.util.List;

public interface UserProfileRepository extends CrudRepository<UserProfileEntity, Integer> {
    List<UserProfileEntity> findUserProfileEntityByUserid(int id);
}
