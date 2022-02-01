package pos.auth.View.Validate;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "status", "role", "id"
})
@XmlRootElement(name = "validateResponse")
@Getter
@Setter
public class ValidateResponse {
    @XmlElement(required = true)
    protected String status;

    @XmlElement(required = true)
    protected String role;

    @XmlElement(required = true)
    protected int id;
}
