package pulse.eco.atmospheriq.entity;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "measurement")
public class Measurement {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column
    private String sensorId;

    @Column
    private int value;

    @Column(nullable = false)
    private String timestamp;

    @Column
    private String type;
}
