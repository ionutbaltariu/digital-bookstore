package pos.auth.soap;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "name",
        "password"
})
@XmlRootElement(name = "registerRequest")
@Getter
@Setter
public class RegisterRequest {

    @XmlElement(required = true)
    protected String name;
    @XmlElement(required = true)
    protected String password;
}
