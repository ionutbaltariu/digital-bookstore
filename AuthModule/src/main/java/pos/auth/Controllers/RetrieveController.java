package pos.auth.Controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;
import pos.auth.Model.DTO.UserWithProfileDTO;
import pos.auth.Services.UserDataService;
import pos.auth.View.RetrieveProfile.RetrieveRequest;
import pos.auth.View.RetrieveProfile.RetrieveResponse;


@Endpoint
public class RetrieveController {
    @Autowired
    private UserDataService userDataService;

    private static final String NAMESPACE_URI = "http://pos.examples.soap.stateless/retrieve";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "retrieveRequest")
    @ResponsePayload
    public RetrieveResponse retrieve(@RequestPayload RetrieveRequest input) throws Exception {
        return constructResponse(userDataService.loadUserWithProfileData(input.getId()));
    }

    RetrieveResponse constructResponse(UserWithProfileDTO userDataContainer){
        RetrieveResponse response = new RetrieveResponse();

        response.setFirstname(userDataContainer.getFirstName());
        response.setLastname(userDataContainer.getLastName());
        response.setEmail(userDataContainer.getEmail());
        response.setAddress(userDataContainer.getAddress());
        response.setBirthday(userDataContainer.getBirthday());
        response.setName(userDataContainer.getUsername());

        return response;
    }
}
