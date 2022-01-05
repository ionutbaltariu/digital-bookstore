package pos.auth.soap;

import javax.xml.bind.annotation.*;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "status",
        "errorMessage"
})
@XmlRootElement(name = "loginResponse")
public class RegisterResponse {
    @XmlElement(required = true)
    protected String status;
    @XmlElement(required = false)
    protected String errorMessage;

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }
}
