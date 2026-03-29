package auth_service.user;

import auth_service.dto.RegistrationRequest;
import auth_service.exception.EmailAlreadyExistsException;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public User createUser(RegistrationRequest request) {
        checkIfUserExists(request.email());
        return saveNewUser(request);
    }

    // NOWE — szukamy usera po ID (expense-service będzie tego używał)
    public Optional<User> findById(UUID id) {
        return userRepository.findById(id);
    }

    private void checkIfUserExists(String email) {
        if (userRepository.existsByEmail(email)) {
            throw new EmailAlreadyExistsException();
        }
    }

    private User saveNewUser(RegistrationRequest request) {
        User user = User.builder()
                .email(request.email())
                .password(passwordEncoder.encode(request.password()))
                .name(request.name())  // NOWE — zapisujemy imię
                .build();

        return userRepository.save(user);
    }
}
