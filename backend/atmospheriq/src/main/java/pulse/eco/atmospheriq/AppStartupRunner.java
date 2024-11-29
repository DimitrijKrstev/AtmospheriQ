package pulse.eco.atmospheriq;

import lombok.AllArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
public class AppStartupRunner implements CommandLineRunner {

    private final PulseEcoClient pulseEcoClient;

    @Override
    public void run(String... args) {
        pulseEcoClient.fetchAndSaveMeasurements();
        System.out.println("Fetched and saved measurements.");
    }
}
