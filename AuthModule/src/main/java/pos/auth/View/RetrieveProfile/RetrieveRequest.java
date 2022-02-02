package pos.auth.View.RetrieveProfile;

import lombok.Getter;
import lombok.Setter;

import javax.xml.bind.annotation.*;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "id",
})
@XmlRootElement(name = "retrieveRequest")
@Getter
@Setter
public class RetrieveRequest {
    @XmlElement(required = true)
    protected int id;
}
