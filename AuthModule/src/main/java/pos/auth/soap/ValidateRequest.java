package pos.auth.soap;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "token",
})
@XmlRootElement(name = "validateRequest")
public class ValidateRequest {
    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

    @XmlElement(required = true)
    protected String token;
}
