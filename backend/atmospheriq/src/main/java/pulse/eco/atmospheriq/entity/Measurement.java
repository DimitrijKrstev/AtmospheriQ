package pulse.eco.atmospheriq.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Table(name = "measurement")
public class Measurement {
    @Id
    @GeneratedValue
    private Long id;

    private String sensorId;

    private String type;

    @Column(nullable = false)
    private String stamp;

    private String position;

    @Column(name = "measurement_value")
    private int value;
}
