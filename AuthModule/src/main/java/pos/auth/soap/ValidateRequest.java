package pos.auth.soap;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "token",
})
@XmlRootElement(name = "validateRequest")
@Getter
@Setter
public class ValidateRequest {
    @XmlElement(required = true)
    protected String token;
}
