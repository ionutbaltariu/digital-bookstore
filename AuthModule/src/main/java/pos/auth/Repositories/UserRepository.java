package pos.auth.Repositories;

import org.springframework.data.repository.CrudRepository;
import pos.auth.Entities.User;

import java.util.List;

public interface UserRepository extends CrudRepository<User, Integer> {
    List<User> findByUsername(String lastName);
    User findById(long id);
}
