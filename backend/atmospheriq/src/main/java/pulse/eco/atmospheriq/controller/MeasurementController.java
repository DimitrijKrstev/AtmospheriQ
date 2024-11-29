package pulse.eco.atmospheriq.controller;

import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;
import pulse.eco.atmospheriq.entity.Measurement;
import pulse.eco.atmospheriq.service.MeasurementService;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/measurements")
public class MeasurementController {

    private final MeasurementService service;

    @GetMapping
    public List<Measurement> getAllMeasurements() {
        return service.getAllMeasurements();
    }

    @PostMapping
    public void saveMeasurements(@RequestBody List<Measurement> measurements) {
        service.saveMeasurements(measurements);
    }
}