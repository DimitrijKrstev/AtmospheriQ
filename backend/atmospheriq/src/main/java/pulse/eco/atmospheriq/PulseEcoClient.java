package pulse.eco.atmospheriq;

import lombok.AllArgsConstructor;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import pulse.eco.atmospheriq.entity.Measurement;
import pulse.eco.atmospheriq.service.MeasurementService;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;

@Component
@AllArgsConstructor
public class PulseEcoClient {

    private final MeasurementService measurementService;

    public void fetchAndSaveMeasurements() {
        String url = "https://skopje.pulse.eco/rest/current";
        RestTemplate restTemplate = new RestTemplate();

        String username = "Dimitrij";
        String password = "codefu2024";
        String base64Credentials = Base64.getEncoder()
                .encodeToString((username + ":" + password).getBytes(StandardCharsets.UTF_8));

        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Basic " + base64Credentials);
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<String> entity = new HttpEntity<>(headers);

        ResponseEntity<Measurement[]> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                entity,
                Measurement[].class
        );

        if (response.getStatusCode() == HttpStatus.OK) {
            List<Measurement> measurements = Arrays.asList(response.getBody());
            measurementService.saveMeasurements(measurements);
        } else {
            System.out.println("Failed to fetch data. Status code: " + response.getStatusCode());
        }
    }

}
