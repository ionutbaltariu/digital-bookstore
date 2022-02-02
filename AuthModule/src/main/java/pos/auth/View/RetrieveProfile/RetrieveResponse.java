package pos.auth.View.RetrieveProfile;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "firstname",
        "lastname",
        "email",
        "address",
        "birthday",
        "name",
})
@XmlRootElement(name = "retrieveResponse")
@Getter
@Setter
public class RetrieveResponse {
    @XmlElement(required = true)
    protected String firstname;
    @XmlElement(required = true)
    protected String lastname;
    @XmlElement(required = true)
    protected String email;
    @XmlElement(required = true)
    protected String address;
    @XmlElement(required = true)
    protected String birthday;
    @XmlElement(required = true)
    protected String name;
}
