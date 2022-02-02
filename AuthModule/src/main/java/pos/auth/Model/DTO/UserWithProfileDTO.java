package pos.auth.Model.DTO;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class UserWithProfileDTO {
    private String firstName;
    private String lastName;
    private String username;
    private String email;
    private String address;
    private String birthday;
}
