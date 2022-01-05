package pos.auth.soap;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "status",
})
@XmlRootElement(name = "validateResponse")
@Getter
@Setter
public class ValidateResponse {
    @XmlElement(required = true)
    protected String status;
}
