package pos.auth.soap;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "name",
        "password"
})
@XmlRootElement(name = "registerRequest")
public class RegisterRequest {

    @XmlElement(required = true)
    protected String name;
    @XmlElement(required = true)
    protected String password;


    public String getName() {
        return name;
    }

    public void setName(String value) {
        this.name = value;
    }

    public String getPassword() {
        return password;
    }


    public void setPassword(String value) {
        this.password = value;
    }

}
