package pulse.eco.atmospheriq.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pulse.eco.atmospheriq.entity.Measurement;

public interface MeasurementRepo extends JpaRepository<Measurement,Long> {
}
