package pos.auth.Model.Repositories;

import org.springframework.data.repository.CrudRepository;
import pos.auth.Model.Entities.UserEntity;

import java.util.List;

public interface UserRepository extends CrudRepository<UserEntity, Integer> {
    List<UserEntity> findByUsername(String lastName);
    UserEntity findById(long id);
}
