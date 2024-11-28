package pulse.eco.atmospheriq.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import pulse.eco.atmospheriq.entity.Sensor;

public interface SensorRepo extends JpaRepository<Sensor,String> {
}
